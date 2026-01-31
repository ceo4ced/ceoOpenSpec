'use client';

import React, { useState } from 'react';
import './TestRunner.css';

interface TestRunnerProps {
    onResultsChange?: (results: any) => void;
}

export default function TestRunner({ onResultsChange }: TestRunnerProps) {
    const [running, setRunning] = useState(false);
    const [results, setResults] = useState<any>(null);

    const runTests = async (type: 'all' | 'components' | 'pages') => {
        setRunning(true);
        setResults(null);

        // Simulate test execution
        // In a real implementation, this would call an API endpoint that runs Jest
        await new Promise(resolve => setTimeout(resolve, 2000));

        const mockResults = {
            type,
            totalTests: type === 'all' ? 45 : type === 'components' ? 30 : 15,
            passed: type === 'all' ? 43 : type === 'components' ? 29 : 14,
            failed: type === 'all' ? 2 : type === 'components' ? 1 : 1,
            coverage: {
                statements: type === 'all' ? 85 : type === 'components' ? 90 : 78,
                branches: type === 'all' ? 82 : type === 'components' ? 88 : 75,
                functions: type === 'all' ? 87 : type === 'components' ? 92 : 80,
                lines: type === 'all' ? 85 : type === 'components' ? 90 : 78,
            },
        };

        setResults(mockResults);
        setRunning(false);

        if (onResultsChange) {
            onResultsChange(mockResults);
        }
    };

    return (
        <div className="test-runner">
            <div className="test-controls">
                <button
                    className="test-btn all"
                    onClick={() => runTests('all')}
                    disabled={running}
                >
                    {running ? '⏳ Running...' : '🧪 Run All Tests'}
                </button>
                <button
                    className="test-btn components"
                    onClick={() => runTests('components')}
                    disabled={running}
                >
                    {running ? '⏳ Running...' : '📦 Test Components'}
                </button>
                <button
                    className="test-btn pages"
                    onClick={() => runTests('pages')}
                    disabled={running}
                >
                    {running ? '⏳ Running...' : '📄 Test Pages'}
                </button>
            </div>

            {results && (
                <div className="test-results">
                    <div className="results-summary">
                        <h3>Test Results ({results.type})</h3>
                        <div className="results-stats">
                            <div className="stat passed">
                                <span className="stat-value">{results.passed}</span>
                                <span className="stat-label">Passed</span>
                            </div>
                            <div className="stat failed">
                                <span className="stat-value">{results.failed}</span>
                                <span className="stat-label">Failed</span>
                            </div>
                            <div className="stat total">
                                <span className="stat-value">{results.totalTests}</span>
                                <span className="stat-label">Total</span>
                            </div>
                        </div>
                    </div>

                    <div className="coverage-section">
                        <h3>Coverage</h3>
                        <div className="coverage-metrics">
                            <div className="coverage-item">
                                <span className="metric-label">Statements</span>
                                <div className="metric-bar">
                                    <div
                                        className="metric-fill"
                                        style={{ width: `${results.coverage.statements}%` }}
                                    />
                                </div>
                                <span className="metric-value">{results.coverage.statements}%</span>
                            </div>
                            <div className="coverage-item">
                                <span className="metric-label">Branches</span>
                                <div className="metric-bar">
                                    <div
                                        className="metric-fill"
                                        style={{ width: `${results.coverage.branches}%` }}
                                    />
                                </div>
                                <span className="metric-value">{results.coverage.branches}%</span>
                            </div>
                            <div className="coverage-item">
                                <span className="metric-label">Functions</span>
                                <div className="metric-bar">
                                    <div
                                        className="metric-fill"
                                        style={{ width: `${results.coverage.functions}%` }}
                                    />
                                </div>
                                <span className="metric-value">{results.coverage.functions}%</span>
                            </div>
                            <div className="coverage-item">
                                <span className="metric-label">Lines</span>
                                <div className="metric-bar">
                                    <div
                                        className="metric-fill"
                                        style={{ width: `${results.coverage.lines}%` }}
                                    />
                                </div>
                                <span className="metric-value">{results.coverage.lines}%</span>
                            </div>
                        </div>
                    </div>

                    <div className="test-commands">
                        <h4>CLI Commands</h4>
                        <code>npm test</code> - Run all tests
                        <br />
                        <code>npm run test:components</code> - Test components only
                        <br />
                        <code>npm run test:pages</code> - Test pages only
                        <br />
                        <code>npm run test:coverage</code> - Generate coverage report
                    </div>
                </div>
            )}
        </div>
    );
}
