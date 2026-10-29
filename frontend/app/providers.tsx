"use client";

import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { ReactNode } from "react";

const theme = createTheme({
  palette: {
    primary: { main: "#5146E5" },
    background: { default: "#F7F7FB" },
  },
  shape: { borderRadius: 10 },
  typography: { fontFamily: "Inter, Arial, sans-serif" },
});

export default function Providers({ children }: { children: ReactNode }) {
  return <ThemeProvider theme={theme}><CssBaseline />{children}</ThemeProvider>;
}
