import React from "react";
import DashboardSidebar from "@/components/DashboardSidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] bg-[#f4f7fa]">
      <DashboardSidebar />
      <div className="flex-1 overflow-y-auto p-6 lg:p-8">
        {children}
      </div>
    </div>
  );
}
