
import Sidebar from "@/components/Sidebar";
import OverlaySuppressor from "@/components/OverlaySuppressor";

export default function MainLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="app-container">
            <OverlaySuppressor />
            <Sidebar />
            {children}
        </div>
    );
}
