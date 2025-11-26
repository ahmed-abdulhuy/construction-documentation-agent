export async function signIn(email: string, password: string) {

  const formData = new URLSearchParams();
  formData.append("grant_type", "password");
  formData.append("username", email);
  formData.append("password", password);
  // formData.append("scope", "");
  // formData.append("client_id", "string");
  // formData.append("client_secret", "string");

  const res = await fetch('http://localhost:8000/login/access-token', {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  const data = await res.json();
  
  return data; // returns user/session/token
}
