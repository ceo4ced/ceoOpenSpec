import styles from './page.module.css';

export default function DevLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className={styles['dev-layout']}>
            <div className={styles['dev-header']}>
                <div className={styles['dev-logo']}>
                    <span className={styles['dev-icon']}>⚙️</span>
                    <span className={styles['dev-title']}>SERVER DASHBOARD</span>
                </div>
            </div>
            {children}
        </div>
    );
}
