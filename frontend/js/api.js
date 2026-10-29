const API_BASE_URL = "http://localhost:8000";

// export makes the function available for import in other js files
// async indicates that the function returns a promise and can be awaited
export async function generatePassword(length) {
    const url = `${API_BASE_URL}/password/generate-pass?length=${length}`;

    console.log("request URL:", url);

    const response = await fetch(url);

    console.log("response status:", response.status);

    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    return data.password;
}