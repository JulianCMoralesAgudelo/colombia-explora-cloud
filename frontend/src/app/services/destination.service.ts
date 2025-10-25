import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { EnvService } from './env.service';

export interface Destination {
    id: number;
    name: string;
    description: string;
    region: string;
    price: number;
    created_at: string;
}

@Injectable({
    providedIn: 'root'
})
export class DestinationService {
    constructor(
        private http: HttpClient,
        private auth: AuthService,
        private env: EnvService
    ) { }

    private getHeaders(): HttpHeaders {
        const token = this.auth.getToken();
        return new HttpHeaders({
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        });
    }

    getDestinations(): Observable<Destination[]> {
        return this.http.get<Destination[]>(`${this.env.getApiUrl()}/destinations`, {
            headers: this.getHeaders()
        });
    }

    createDestination(destination: Omit<Destination, 'id' | 'created_at'>): Observable<Destination> {
        return this.http.post<Destination>(`${this.env.getApiUrl()}/destinations`, destination, {
            headers: this.getHeaders()
        });
    }

    updateDestination(id: number, updates: Partial<Destination>): Observable<Destination> {
        return this.http.patch<Destination>(`${this.env.getApiUrl()}/destinations/${id}`, updates, {
            headers: this.getHeaders()
        });
    }

    deleteDestination(id: number): Observable<any> {
        return this.http.delete(`${this.env.getApiUrl()}/destinations/${id}`, {
            headers: this.getHeaders()
        });
    }
}