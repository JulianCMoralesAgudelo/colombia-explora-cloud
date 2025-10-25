import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";

@Injectable({
    providedIn: "root",
})
export class EnvService {
    private apiUrl: string;
    private authUrl: string;

    constructor() {
        // En producción, usar URLs de API Gateway
        if (environment.production) {
            this.apiUrl =
                "https://" + (window as any).API_GATEWAY_URL || environment.apiUrl;
            this.authUrl =
                "https://" + (window as any).API_GATEWAY_URL + "/auth" ||
                environment.authUrl;
        } else {
            this.apiUrl = environment.apiUrl;
            this.authUrl = environment.authUrl;
        }
    }

    getApiUrl(): string {
        return this.apiUrl;
    }

    getAuthUrl(): string {
        return this.authUrl;
    }
}
