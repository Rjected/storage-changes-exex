//! storage_histogram_exex is a reth [Execution Extension](https://www.paradigm.xyz/2024/05/reth-exex)
//! which creates a histogram of storage changes, per account, per commit

#![cfg_attr(not(test), warn(unused_crate_dependencies))]

use csv::Writer;
use futures::Future;
use reth_exex::{ExExContext, ExExNotification};
use reth_node_api::FullNodeComponents;
use reth_node_ethereum::EthereumNode;
use reth_primitives::Address;
use std::collections::HashMap;
use std::fs::File;
use tracing::info;

/// This creates a histogram of storage changes per account on every committed chain, which is then
/// saved as a csv file.
async fn storage_histogram_exex<Node: FullNodeComponents>(
    mut ctx: ExExContext<Node>,
) -> eyre::Result<()> {
    while let Some(notification) = ctx.notifications.recv().await {
        if let ExExNotification::ChainCommitted { new } = notification {
            let block_number = new.blocks().keys().next_back().unwrap().to_string();
            let mut storage_changes_histogram: HashMap<Address, usize> = HashMap::new();

            // collect the storage changes
            for (account, account_info) in new.state().bundle_accounts_iter() {
                let changes = account_info.storage.len();
                storage_changes_histogram.entry(account).or_insert(changes);
            }

            // save in the assets folder
            let file_name = format!("assets/block_{}_storage_changes.csv", block_number);
            let file = File::create(&file_name)?;
            let mut wtr = Writer::from_writer(file);

            wtr.write_record(["account", "changes"])?;

            for (account, changes) in &storage_changes_histogram {
                wtr.write_record(&[hex::encode(account), changes.to_string()])?;
            }
            wtr.flush()?;

            info!("Saved storage change histogram to {}", file_name);
        }
    }
    Ok(())
}

/// The initialization logic of the ExEx is just an async function.
pub async fn init<Node: FullNodeComponents>(
    ctx: ExExContext<Node>,
) -> eyre::Result<impl Future<Output = eyre::Result<()>>> {
    info!("Initialized StorageHistogramExEx");

    Ok(async move {
        storage_histogram_exex(ctx).await?;
        Ok(())
    })
}

fn main() -> eyre::Result<()> {
    reth::cli::Cli::parse_args().run(|builder, _| async move {
        let handle = builder
            .node(EthereumNode::default())
            .install_exex("StorageHistogram", init)
            .launch()
            .await?;

        handle.wait_for_node_exit().await
    })
}
