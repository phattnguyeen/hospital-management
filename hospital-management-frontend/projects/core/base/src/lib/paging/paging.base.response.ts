import { propertyMapper } from "../mapper/property.mapper";

/**
 * Defines Paging BO Base
 */
export class PagingBaseResponse {
  @propertyMapper('activePage', Number)
  activePage: number = 0;

  @propertyMapper('totalPages', Number)
  totalPages: number = 0;

  @propertyMapper('totalItems', Number)
  totalItems: number = 0;

  @propertyMapper('pageSize', Number)
  pageSize: number = 0;

  constructor(init: Partial<PagingBaseResponse> = {}) {
    Object.assign(this, init);
  }
}
