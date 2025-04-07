import { inject, Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { BROWSER_STORAGE } from '@infrastructure/base';
import { AuthorizationConstant } from './authorization.constant';

@Injectable({
  providedIn: 'root',
})
export class AuthorizationGuard implements CanActivate {
  private readonly router = inject(Router);
  private readonly storage = inject(BROWSER_STORAGE);

  /**
   * Redirects the user to the sign-in page.
   *
   * @private
   */
  private redirectToSignIn(): boolean {
    this.router.navigateByUrl('/sign-in');
    return false;
  }

   /**
   * Checks whether the user is authorized to access a route.
   *
   * @param route The route being accessed.
   * @param state The current router state.
   * @returns Promise<boolean> Whether the route can be activated.
   */
  async canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
     const isAuthenticated = !!this.storage.get(AuthorizationConstant.accessToken); // Check if the user is authenticated
    if (isAuthenticated) {
      return true;
    } else {
        return this.redirectToSignIn(); // Redirect to login if not authenticated
    }
  }
}
