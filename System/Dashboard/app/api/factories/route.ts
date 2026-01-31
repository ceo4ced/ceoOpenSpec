import { NextResponse } from 'next/server';
import { getFactories, saveFactory, Factory } from '../../../lib/factory';
import { exec } from 'child_process';
import util from 'util';
import path from 'path';

const execPromise = util.promisify(exec);

export async function GET() {
    try {
        const factories = getFactories();
        return NextResponse.json(factories);
    } catch (error) {
        return NextResponse.json({ error: 'Failed to fetch factories' }, { status: 500 });
    }
}

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { name, domain, owner } = body;

        if (!name || !domain) {
            return NextResponse.json({ error: 'Name and domain are required' }, { status: 400 });
        }

        // 1. Create a minimal factory record
        const newFactory: Factory = {
            id: crypto.randomUUID(),
            name,
            domain,
            repo_url: `https://github.com/${owner || 'unknown'}/${name}`,
            status: 'development',
            created_at: new Date().toISOString(),
            useFakeData: body.useFakeData,
        };

        // 2. Mock File Creation / Fake Data Population
        // In a real app, this would be: await populateFactory(newFactory.name, newFactory.useFakeData);
        // For now, we assume the folder creation is external or manual, 
        // OR we can implement a basic scaffold here if we had write access to a parent dir.
        // Given we are in the Dashboard App, let's just log it for the prototype.

        if (body.useFakeData) {
            console.log(`[ONBOARDING BYPASS] Populating ${name} with fake data...`);
            // Logic to write .mission/mission-statement.md, etc. would go here.
            // Example:
            // fs.writeFileSync(path.join(factoryPath, '.mission/mission-statement.md'), 'We make widgets.');
        }

        // 2. Execute gh command to create repo (this is a simplified implementation)
        // In a real scenario, we would clone the current repo, replace string, and push.
        // For now, we'll try to create the repo if gh is available.

        try {
            // Attempt to create repo using gh CLI
            // Note: This relies on the server having gh auth'd
            if (owner) {
                // This is a placeholder for the actual complex logic of cloning/pushing
                // For the MVC, we will just record it in the DB.
            }
        } catch (e) {
            console.error('Failed to create repo via CLI:', e);
            // Continue even if CLI fails, just creation record locally
        }

        saveFactory(newFactory);

        return NextResponse.json(newFactory);
    } catch (error) {
        console.error('Error creating factory:', error);
        return NextResponse.json({ error: 'Failed to create factory' }, { status: 500 });
    }
}
