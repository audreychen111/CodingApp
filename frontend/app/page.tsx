"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/health/`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("error: could not reach backend"));
  }, []);

  return (
    <main>
      <h1>Backend status: {status}</h1>
    </main>
  );
}
