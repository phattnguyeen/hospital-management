import { IReadableRepository } from '@core/base';
import { AssetRequest } from '@core/models';
import { Observable } from 'rxjs';

export interface IAssetReadableRepository extends IReadableRepository {
  getAsset(request: AssetRequest): Observable<any>;
}
