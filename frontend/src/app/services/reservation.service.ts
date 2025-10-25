import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { EnvService } from './env.service';

export interface Reservation {
    id: number;
    people: number;
    check_in: string;
    check_out: string;
    total_price: number;
    created_at: string;
    destination_name: string;
    region: string;
    destination_price: number;
}

export interface CreateReservation {
    destination_id: number;
    people: number;
    check_in: string;
    check_out: string;
}

@Injectable({
    providedIn: 'root'
})
export class ReservationService {
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

    getReservations(): Observable<Reservation[]> {
        return this.http.get<Reservation[]>(`${this.env.getApiUrl()}/reservations`, {
            headers: this.getHeaders()
        });
    }

    createReservation(reservation: CreateReservation): Observable<Reservation> {
        return this.http.post<Reservation>(`${this.env.getApiUrl()}/reservations`, reservation, {
            headers: this.getHeaders()
        });
    }
}