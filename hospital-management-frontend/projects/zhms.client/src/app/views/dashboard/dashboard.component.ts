import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'hms-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  standalone: true,
})
export class DashboardComponent implements OnInit {
  constructor(private router: Router) {}

  logout() {
    // Add any necessary logout logic here, such as clearing user data or tokens
    localStorage.removeItem('access_token');
    // Navigate to the login page
    this.router.navigate(['/login']);
  }

  ngOnInit(): void {}
}
