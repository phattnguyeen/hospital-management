import { InjectionToken } from '@angular/core';
import { IReadableRepository } from './interface.readable.repository';
import { IWriteableRepository } from './interface.writeable.repository';

/**
 * Define Repository which combine all actions
 * Readable  -> Read Repository
 * Writeable -> Write Repository
 */
export interface IBaseRepository extends IReadableRepository, IWriteableRepository {}

export const BASE_REPOSITORY = new InjectionToken<IBaseRepository>('BASE_REPOSITORY');
