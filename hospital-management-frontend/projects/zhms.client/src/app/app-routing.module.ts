import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthorizationGuard } from '@infrastructure/authorization';

export const routes: Routes = [
  {
    path: 'sign-in',
    loadComponent: () => import('./views/sign-in/sign-in.component').then((c) => c.SignInComponent),
  },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () => import('./views/dashboard/dashboard.component').then((c) => c.DashboardComponent),
    canActivate: [AuthorizationGuard],
  },
  {
    path: 'home',
    loadComponent: () => import('./views/home/home.component').then((c) => c.HomeComponent),
    canActivate: [AuthorizationGuard],
  },
  { path: '**', redirectTo: '/page-not-found' },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      bindToComponentInputs: true,
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
