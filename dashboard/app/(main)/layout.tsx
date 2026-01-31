
import Sidebar from "@/components/Sidebar";

export default function MainLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="app-container">
            <Sidebar />
            {children}
        </div>
    );
}
