// filepath: /E:/Master/High-Software/Hospital-Web/hospital-management-frontend/src/app/account/login/login.component.ts
import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { initThreeScene } from 'src/app/three/three-scene';
import { LogoService } from 'src/app/service/logo.service';
import { ApiService } from 'src/app/service/api.service';
import lottie from 'lottie-web';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, AfterViewInit {
  @ViewChild('threeContainer', { static: true }) threeContainer!: ElementRef;
  @ViewChild('logoContainer', { static: true }) logoContainer!: ElementRef;

  username: string = '';
  password: string = '';
  errorMessage: string | null = null;

  constructor(private logoService: LogoService, private apiService: ApiService, private router: Router) { }

  ngOnInit(): void {
    this.logoService.getLogo().subscribe(data => {
      lottie.loadAnimation({
        container: this.logoContainer.nativeElement,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: data // Adjust this based on the structure of your JSON
      });
    });
  }

  ngAfterViewInit() {
    if (this.threeContainer) {
      initThreeScene(this.threeContainer.nativeElement);
    }
  }

  login() {
    this.apiService.login({ username: this.username, password: this.password }).subscribe(
      response => {
        console.log('Login Success:', response);
        localStorage.setItem('access_token', response.access_token); // Store token
        this.router.navigate(['/dashboard']); // Navigate after login
      },
      error => {
        console.error('Login Failed:', error);
        this.errorMessage = 'Invalid username or password';
      }
    );
  }
}