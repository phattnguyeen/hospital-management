import { propertyMapper } from "../mapper/property.mapper";

export class PagingBaseRequest {
  @propertyMapper('Page', Number)
  page: number = 1;

  @propertyMapper('PageSize', Number)
  pageSize: number = 16;

  @propertyMapper('Sort', String)
  sort: string = '';

  @propertyMapper('Filters', String)
  filters: string = '';

  constructor(init: Partial<PagingBaseRequest> = {}) {
    Object.assign(this, init);
  }
}
