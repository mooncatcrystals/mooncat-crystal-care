// Adds someone who asked for the printable care chart to Flodesk.
// The Flodesk "Crystal Care Chart" workflow (trigger: added to the segment in
// FLODESK_SEGMENT_CARE) emails them the chart link. The API key lives only in
// the Cloudflare Pages environment, never in the page.

const FLODESK_API_URL = "https://api.flodesk.com/v1/subscribers";

function respond(status, data) {
  return new Response(JSON.stringify(data), {
    status: status,
    headers: { "Content-Type": "application/json" }
  });
}

function isValidEmail(email) {
  return typeof email === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// First names end up in an email Flodesk sends, so only accept something that
// looks like a name; anything else (a URL, spam) is dropped.
function cleanFirstName(name) {
  const trimmed = (name || "").trim();
  if (!trimmed || trimmed.length > 40) return "";
  if (!/^[\p{L}][\p{L}\p{M} '’-]*$/u.test(trimmed)) return "";
  return trimmed;
}

export async function onRequestPost(context) {
  const env = context.env;
  let payload;
  try {
    payload = await context.request.json();
  } catch (err) {
    return respond(400, { ok: false, error: "Invalid JSON" });
  }

  const email = (payload.email || "").trim();
  const firstName = cleanFirstName(payload.firstName);
  if (!isValidEmail(email)) return respond(400, { ok: false, error: "Invalid email" });

  if (!env.FLODESK_API_KEY || !env.FLODESK_SEGMENT_CARE) {
    console.error("FLODESK_API_KEY or FLODESK_SEGMENT_CARE is not set in the Cloudflare Pages environment.");
    return respond(500, { ok: false, error: "Server not configured" });
  }

  const body = { email: email, segment_ids: [env.FLODESK_SEGMENT_CARE] };
  if (firstName) body.first_name = firstName;

  try {
    const res = await fetch(FLODESK_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Basic " + btoa(env.FLODESK_API_KEY + ":")
      },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      const detail = (res.status + " " + (await res.text())).slice(0, 300);
      console.error("Flodesk API error", detail);
      return respond(502, { ok: false, error: "Flodesk API error", flodeskError: detail });
    }
    return respond(200, { ok: true });
  } catch (err) {
    console.error("Error calling Flodesk API", err);
    return respond(500, { ok: false, error: "Unexpected error" });
  }
}
