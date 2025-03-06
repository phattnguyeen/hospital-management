import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(private router: Router) {}

  isHomePage(): boolean {
    return this.router.url === '/home';
  }

  isDashboardPage(): boolean {
    return this.router.url === '/dashboard';
  }

  isLoginPage(): boolean {
    return this.router.url === '/login';
  }
}