
export function setToken(token: string) {
    localStorage.setItem('token', token);
}

export function setRefreshToken(token: string) {
    localStorage.setItem('refreshToken', token);
}

export function getToken(): string | null {
    return localStorage.getItem('token');
}

export function getRefreshToken(): string | null {
    return localStorage.getItem('refreshToken');
}

export function removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
}

export function isLoggedIn(): boolean {
    return !!getToken();
}
