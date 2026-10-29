import type { Metadata } from "next";
import Providers from "./providers";
export const metadata: Metadata = { title: "Candidate Connect", description: "Recruiter communication platform" };
export default function Layout({ children }: { children: React.ReactNode }) { return <html lang="en"><body><Providers>{children}</Providers></body></html>; }
