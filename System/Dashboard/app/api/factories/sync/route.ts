import { NextResponse } from 'next/server';
import { syncFactory, syncAllFactories } from '../../../lib/sync';
import { getFactories } from '../../../lib/factory';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { factoryId, syncAll } = body;

        if (syncAll) {
            const results = await syncAllFactories();
            return NextResponse.json({ results });
        }

        if (factoryId) {
            const factories = getFactories();
            const factory = factories.find(f => f.id === factoryId);

            if (!factory) {
                return NextResponse.json({ error: 'Factory not found' }, { status: 404 });
            }

            const result = await syncFactory(factory);
            return NextResponse.json({ result });
        }

        return NextResponse.json({ error: 'Invalid request' }, { status: 400 });

    } catch (error) {
        console.error('Sync failed:', error);
        return NextResponse.json({ error: 'Sync failed' }, { status: 500 });
    }
}
