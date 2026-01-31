'use client';

import React, { useState, useEffect } from 'react';
import styles from '../app/dev/page.module.css';

interface Factory {
    id: string;
    name: string;
    repo_url: string;
    domain: string;
    status: 'development' | 'production';
    created_at: string;
}

export default function FactoryManager() {
    const [factories, setFactories] = useState<Factory[]>([]);
    const [loading, setLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [newFactory, setNewFactory] = useState({ name: '', domain: '', owner: '', useFakeData: false });

    const [syncing, setSyncing] = useState<string | null>(null); // 'all' or factoryId

    useEffect(() => {
        fetchFactories();
    }, []);

    const fetchFactories = async () => {
        try {
            const res = await fetch('/api/factories');
            if (res.ok) {
                const data = await res.json();
                setFactories(data);
            }
        } catch (error) {
            console.error('Failed to fetch factories', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsCreating(true);
        try {
            const res = await fetch('/api/factories', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newFactory),
            });
            if (res.ok) {
                await fetchFactories();
                setNewFactory({ name: '', domain: '', owner: '', useFakeData: false });
            } else {
                alert('Failed to create factory');
            }
        } catch (error) {
            console.error('Error creating factory', error);
        } finally {
            setIsCreating(false);
        }
    };

    const handleSync = async (factoryId?: string) => {
        setSyncing(factoryId || 'all');
        try {
            const res = await fetch('/api/factories/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ factoryId, syncAll: !factoryId }),
            });
            if (res.ok) {
                const data = await res.json();
                console.log('Sync result:', data);
                // Ideally show a toast or notification here
            } else {
                alert('Sync failed');
            }
        } catch (error) {
            console.error('Sync error', error);
        } finally {
            setSyncing(null);
        }
    };

    return (
        <div className={styles.factoryManager}>
            <div className={styles.panelHeader}>
                <h2 className={styles.sectionTitle}>
                    FACTORY REPLICATION SYSTEM
                </h2>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <button
                        onClick={() => handleSync()}
                        disabled={!!syncing}
                        style={{
                            background: 'transparent',
                            border: '1px solid #333',
                            color: '#888',
                            padding: '4px 8px',
                            fontSize: '0.7rem',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '5px'
                        }}
                    >
                        {syncing === 'all' ? 'SYNCING NETWORK...' : 'SYNC ALL FACTORIES'}
                    </button>
                    <div className={styles.statusBadge}>SYSTEM OPTIMAL</div>
                </div>
            </div>

            <div className={styles.factoryControls}>
                <div className={styles.controlPanel}>
                    <h3 className={styles.controlTitle}>Create New Instance</h3>
                    <form onSubmit={handleCreate} className={styles.createForm}>
                        <div className={styles.inputGroup}>
                            <label>Business Name</label>
                            <input
                                type="text"
                                placeholder="e.g. Acme Corp"
                                value={newFactory.name}
                                onChange={e => setNewFactory({ ...newFactory, name: e.target.value })}
                                required
                            />
                        </div>
                        <div className={styles.inputGroup}>
                            <label>Domain</label>
                            <input
                                type="text"
                                placeholder="e.g. acmecorp.com"
                                value={newFactory.domain}
                                onChange={e => setNewFactory({ ...newFactory, domain: e.target.value })}
                                required
                            />
                        </div>
                        <div className={styles.inputGroup}>
                            <label>GitHub Owner (Optional)</label>
                            <input
                                type="text"
                                placeholder="Organization or User"
                                value={newFactory.owner}
                                onChange={e => setNewFactory({ ...newFactory, owner: e.target.value })}
                            />
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                            <input
                                type="checkbox"
                                id="bypass"
                                checked={newFactory.useFakeData}
                                onChange={e => setNewFactory({ ...newFactory, useFakeData: e.target.checked })}
                                style={{ width: 'auto' }}
                            />
                            <label htmlFor="bypass" style={{ fontSize: '0.75rem', color: '#888' }}>
                                Bypass Onboarding (Use Fake Data)
                            </label>
                        </div>

                        <button type="submit" disabled={isCreating} className={styles.actionButton}>
                            {isCreating ? 'Provisioning...' : 'Provision Factory'}
                        </button>
                    </form>
                </div>

                <div className={styles.monitorPanel}>
                    <div className={styles.tableWrapper}>
                        <table className={styles.factoryTable}>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>NAME</th>
                                    <th>DOMAIN</th>
                                    <th>STATUS</th>
                                    <th>SOURCE</th>
                                    <th>ACTIONS</th>
                                </tr>
                            </thead>
                            <tbody>
                                {factories.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className={styles.emptyState}>No registered factories found. use the control panel to create one.</td>
                                    </tr>
                                ) : (
                                    factories.map(factory => (
                                        <tr key={factory.id}>
                                            <td className={styles.mono}>{factory.id.substring(0, 8)}</td>
                                            <td className={styles.highlight}>{factory.name}</td>
                                            <td>{factory.domain}</td>
                                            <td>
                                                <span className={`${styles.statusDot} ${styles[factory.status]}`}></span>
                                                {factory.status}
                                            </td>
                                            <td>
                                                <a href={factory.repo_url} target="_blank" rel="noopener noreferrer" className={styles.repoLink}>
                                                    View Repository
                                                </a>
                                            </td>
                                            <td>
                                                <button
                                                    onClick={() => handleSync(factory.id)}
                                                    disabled={!!syncing}
                                                    style={{
                                                        background: 'transparent',
                                                        border: 'none',
                                                        color: '#3b82f6',
                                                        cursor: 'pointer',
                                                        fontSize: '0.75rem',
                                                        textDecoration: 'underline'
                                                    }}
                                                >
                                                    {syncing === factory.id ? 'Syncing...' : 'Sync Template'}
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
