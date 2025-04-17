import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { VIEW_CONTEXT } from '@view/base';
import { SignInContext } from '../sign-in/sign-in.context';
@Component({
  selector: 'hms-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, MatSelectModule, MatInputModule, MatSlideToggleModule, MatButtonModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  providers: [{ provide: VIEW_CONTEXT, useExisting: SignInContext }],
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
