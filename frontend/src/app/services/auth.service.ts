import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { EnvService } from './env.service';

export interface User {
    id: number;
    username: string;
    email: string;
    role: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user: User;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private currentUserSubject = new BehaviorSubject<User | null>(null);
    public currentUser$ = this.currentUserSubject.asObservable();

    constructor(private http: HttpClient, private env: EnvService) {
        this.loadStoredUser();
    }

    private loadStoredUser() {
        const token = localStorage.getItem('access_token');
        const userStr = localStorage.getItem('current_user');
        if (token && userStr) {
            this.currentUserSubject.next(JSON.parse(userStr));
        }
    }

    register(username: string, email: string, password: string): Observable<AuthResponse> {
        return this.http.post<AuthResponse>(`${this.env.getAuthUrl()}/register`, {
            username,
            email,
            password
        }).pipe(
            tap(response => this.setSession(response))
        );
    }

    login(username: string, password: string): Observable<AuthResponse> {
        return this.http.post<AuthResponse>(`${this.env.getAuthUrl()}/token`, {
            username,
            password
        }).pipe(
            tap(response => this.setSession(response))
        );
    }

    private setSession(authResult: AuthResponse) {
        localStorage.setItem('access_token', authResult.access_token);
        localStorage.setItem('current_user', JSON.stringify(authResult.user));
        this.currentUserSubject.next(authResult.user);
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('current_user');
        this.currentUserSubject.next(null);
    }

    getToken(): string | null {
        return localStorage.getItem('access_token');
    }

    getCurrentUser(): User | null {
        return this.currentUserSubject.value;
    }

    isAdmin(): boolean {
        return this.currentUserSubject.value?.role === 'admin';
    }

    isLoggedIn(): boolean {
        return !!this.getToken();
    }
}