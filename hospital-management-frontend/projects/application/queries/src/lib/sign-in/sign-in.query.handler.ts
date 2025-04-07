import { inject, Injectable } from '@angular/core';
import { RequestHandler } from '@application/base';
import { SignInErrorResponse, SignInRequest, SignInResponse } from '@core/models';
import { SignInReadableRepository } from '@infrastructure/repositories';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SignInQueryHandler implements RequestHandler<SignInRequest, SignInResponse | SignInErrorResponse> {
  private readonly _signInRepository = inject(SignInReadableRepository);

  /**
   * Handles the sign-in request by calling the sign-in repository and processing the response.
   *
   * @param {SignInRequest} request - The sign-in request containing user credentials.
   * @returns {Observable<SignInResponse | SignInErrorResponse>} An observable that emits either a successful sign-in response or an error response.
   */
  public handle(request: SignInRequest): Observable<SignInResponse | SignInErrorResponse> {
    const result = this._signInRepository.signIn(request);
    return result;
  }
}
