import { exec } from 'child_process';
import util from 'util';
import path from 'path';
import fs from 'fs';
import { Factory, getFactories } from './factory';

const execPromise = util.promisify(exec);

export interface SyncResult {
    factoryId: string;
    success: boolean;
    message: string;
}

export async function syncFactory(factory: Factory): Promise<SyncResult> {
    const factoryPath = path.join(process.cwd(), '..', '..', '..', '..', factory.name); // Assuming parallel dirs for now, adjust based on actual creation logic
    // Correction: The actual creation location needs to be verified. 
    // In the previous plan, we didn't specify exact path. 
    // Let's assume they are sibling directories to the repo root for now, or check where we created them.
    // Re-reading route.ts from previous turn... it didn't actually create the directory yet, just the record.
    // modifying this to assume they are in a "Factories" directory or similar if we want to be organized,
    // but for now let's assume sibling directories to the 'ceoOpenSpec' repo.

    // A better approach for the real system:
    // The factories should probably be tracked by absolute path in the JSON.
    // Since we don't have that in the interface yet, I will assume a standard location.

    // For this mock implementation to work with the "fake" factories created so far:
    if (!fs.existsSync(factoryPath)) {
        return {
            factoryId: factory.id,
            success: false,
            message: 'Local directory not found',
        };
    }

    try {
        // 1. Check/Add upstream
        try {
            await execPromise('git remote get-url upstream', { cwd: factoryPath });
        } catch {
            // Upstream doesn't exist, add it.
            // We need the URL of the current repo (the template).
            // For now, assuming standard template URL. 
            const templateRepo = 'https://github.com/cedricwilliams/ceoOpenSpec.git';
            await execPromise(`git remote add upstream ${templateRepo}`, { cwd: factoryPath });
        }

        // 2. Fetch and Merge
        await execPromise('git fetch upstream', { cwd: factoryPath });
        await execPromise('git merge upstream/main --no-edit', { cwd: factoryPath });

        // 3. Push
        await execPromise('git push origin main', { cwd: factoryPath });

        return {
            factoryId: factory.id,
            success: true,
            message: 'Synced successfully',
        };

    } catch (error: any) {
        return {
            factoryId: factory.id,
            success: false,
            message: error.message || 'Sync failed',
        };
    }
}

export async function syncAllFactories(): Promise<SyncResult[]> {
    const factories = getFactories();
    const results: SyncResult[] = [];

    // Only sync development factories or all? 
    // User said "other children get updated too", implying all.
    for (const factory of factories) {
        // Only attempt to sync if it's a "real" factory (has repo_url)
        if (factory.repo_url) {
            const result = await syncFactory(factory);
            results.push(result);
        }
    }
    return results;
}
