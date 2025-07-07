import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const payload = await req.json();

  try {
    const upstream = await fetch(process.env.BACKEND_URL!, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!upstream.ok) {
      throw new Error(`Backend responded with ${upstream.status}`);
    }

    const data = await upstream.json();

    return new Response(JSON.stringify(data), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
      },
    });
  } catch (error) {
    console.error("Error fetching from backend:", error);
    return new Response(
      JSON.stringify({ error: "Error al procesar la solicitud" }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
