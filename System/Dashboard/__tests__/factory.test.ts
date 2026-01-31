import { saveFactory, getFactories, Factory } from '../lib/factory';
import fs from 'fs';
import path from 'path';

// Mock fs
jest.mock('fs');

describe('Factory System', () => {
    const mockFactory: Factory = {
        id: 'test-id-123',
        name: 'Test Factory',
        domain: 'test.com',
        repo_url: 'https://github.com/test/factory',
        status: 'development',
        created_at: '2023-01-01T00:00:00Z',
        useFakeData: false
    };

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('saveFactory should write to data file', () => {
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.readFileSync as jest.Mock).mockReturnValue('[]');
        (fs.writeFileSync as jest.Mock).mockImplementation(() => { });

        saveFactory(mockFactory);

        expect(fs.writeFileSync).toHaveBeenCalled();
        const callArgs = (fs.writeFileSync as jest.Mock).mock.calls[0];
        const writtenData = JSON.parse(callArgs[1]);

        expect(writtenData).toHaveLength(1);
        expect(writtenData[0].name).toBe('Test Factory');
    });

    test('getFactories should return parsed data', () => {
        (fs.existsSync as jest.Mock).mockReturnValue(true);
        (fs.readFileSync as jest.Mock).mockReturnValue(JSON.stringify([mockFactory]));

        const factories = getFactories();

        expect(factories).toHaveLength(1);
        expect(factories[0].id).toBe('test-id-123');
    });

    test('getFactories should handle empty/missing file', () => {
        (fs.existsSync as jest.Mock).mockReturnValue(false);
        const factories = getFactories();
        expect(factories).toHaveLength(0);
    });
});
