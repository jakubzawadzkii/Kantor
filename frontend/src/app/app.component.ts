import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AppService } from './app.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  data: any[] = [];

  year?: number;
  month?: number;
  day?: number;

  constructor(private service: AppService) { }

  ngOnInit() {
  }

  fetch() {
    this.service.fetch().subscribe(() => {
      this.load();
    });
  }

  load() {
    this.service.getAll(this.year, this.month, this.day)
      .subscribe((res: any) => {
        this.data = res;
      });
  }
}