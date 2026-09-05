import type { Metadata } from 'next'
import './globals.css'
export const metadata:Metadata={title:'CloudOps AIOps — Reliability Command Center',description:'Interactive cloud reliability, anomaly, change-impact, service-health, and runbook decision support.'}
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
