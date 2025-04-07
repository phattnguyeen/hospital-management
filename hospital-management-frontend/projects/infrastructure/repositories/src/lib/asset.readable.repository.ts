import { Injectable } from '@angular/core';
import { IAssetReadableRepository } from '@core/domain';
import { AssetRequest } from '@core/models';
import { ReadableRepository } from '@infrastructure/base';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AssetReadableRepository extends ReadableRepository implements IAssetReadableRepository {
  getAsset(request: AssetRequest): Observable<any> {
    const endPoint = `./images/json/${request.name}`;
    return this.findAll(endPoint);
  }
}
