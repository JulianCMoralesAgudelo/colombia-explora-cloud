import { Component } from '@angular/core';

@Component({
    selector: 'app-root',
    template: `
    <div class="app-container">
      <h1>🏔️ Colombia Explora</h1>
      <p>Migración a AWS en progreso...</p>
      <p>El frontend se está construyendo para despliegue en S3 + CloudFront</p>
    </div>
  `,
    styles: [`
    .app-container {
      text-align: center;
      padding: 50px;
      font-family: Arial, sans-serif;
    }
    h1 {
      color: #2d5f7e;
    }
  `]
})
export class AppComponent {
    title = 'colombia-explora';
}