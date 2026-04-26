import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TallerService } from '../../core/services/taller.service';
import { TallerResponse } from '../../core/models/taller.model';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

@Component({
  selector: 'app-talleres-lista',
  standalone: true,
  imports: [CommonModule, NavbarComponent],
  templateUrl: './talleres-lista.component.html',
  styleUrl: './talleres-lista.component.css',
})
export class TalleresListaComponent implements OnInit {
  private service = inject(TallerService);
  talleres: TallerResponse[] = [];
  loading = true;

  ngOnInit() {
    this.service.listar().subscribe({
      next: (data) => { this.talleres = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }
}
