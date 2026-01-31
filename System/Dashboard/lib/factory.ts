import fs from 'fs';
import path from 'path';

const DATA_FILE = path.join(process.cwd(), 'lib/data/factories.json');

export interface Factory {
    id: string;
    name: string;
    repo_url: string;
    domain: string;
    status: 'development' | 'production';
    created_at: string;
    useFakeData?: boolean;
}

export function getFactories(): Factory[] {
    if (!fs.existsSync(DATA_FILE)) {
        return [];
    }
    const data = fs.readFileSync(DATA_FILE, 'utf-8');
    try {
        return JSON.parse(data);
    } catch (e) {
        return [];
    }
}

export function saveFactory(factory: Factory): void {
    const factories = getFactories();
    factories.push(factory);
    fs.writeFileSync(DATA_FILE, JSON.stringify(factories, null, 2));
}

export function updateFactoryStatus(id: string, status: 'development' | 'production'): void {
    const factories = getFactories();
    const factory = factories.find(f => f.id === id);
    if (factory) {
        factory.status = status;
        fs.writeFileSync(DATA_FILE, JSON.stringify(factories, null, 2));
    }
}

// Logic to populate fake data would typically go here or be called from the route
// Since we are mocking the filesystem creation in the route for now (MVP),
// we will just define the shape here. 
// In a full implementation, this would read files and replace strings.
