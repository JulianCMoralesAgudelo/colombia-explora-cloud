import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="app-container">
      <header>
        <h1>🏔️ Colombia Explora</h1>
        <p>Plataforma de Turismo - Migración AWS</p>
      </header>
      
      <main>
        <div class="status-card">
          <h2>🚀 Estado del Despliegue</h2>
          <p><strong>Frontend:</strong> Angular 15</p>
          <p><strong>Backend:</strong> Python + Lambda</p>
          <p><strong>Base de datos:</strong> PostgreSQL RDS</p>
          <p><strong>Infraestructura:</strong> CloudFormation</p>
        </div>
        
        <div class="next-steps">
          <h3>Próximos pasos:</h3>
          <ul>
            <li>✅ Backend Lambda configurado</li>
            <li>✅ Template CloudFormation listo</li>
            <li>🔄 Frontend en desarrollo</li>
            <li>🔜 Despliegue en AWS</li>
          </ul>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      font-family: Arial, sans-serif;
    }
    header {
      text-align: center;
      margin-bottom: 40px;
    }
    h1 {
      color: #2d5f7e;
      margin-bottom: 10px;
    }
    .status-card {
      background: #f5f5f5;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 20px;
    }
    .next-steps {
      background: #e8f4f8;
      padding: 20px;
      border-radius: 8px;
    }
  `]
})
export class AppComponent {
  title = 'colombia-explora';
}