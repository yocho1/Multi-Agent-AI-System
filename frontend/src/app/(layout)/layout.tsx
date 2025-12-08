import { Header } from "@/components/header";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <main className="min-h-[calc(100vh-56px)]">{children}</main>
    </>
  );
}
