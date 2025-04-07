import { inject, Injectable } from '@angular/core';
import { RequestHandler } from '@application/base';
import { AssetRequest, SignInErrorResponse, SignInRequest, SignInResponse } from '@core/models';
import { AssetReadableRepository, SignInReadableRepository } from '@infrastructure/repositories';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AssetQueryHandler implements RequestHandler<AssetRequest, any> {
  private readonly _assetReadableRepository = inject(AssetReadableRepository);

  /**
   * Handles the sign-in request by calling the sign-in repository and processing the response.
   *
   * @param {SignInRequest} request - The sign-in request containing user credentials.
   * @returns {Observable<SignInResponse | SignInErrorResponse>} An observable that emits either a successful sign-in response or an error response.
   */
  public handle(request: AssetRequest): Observable<any> {
    return this._assetReadableRepository.getAsset(request);
  }
}
