import { InjectionToken } from '@angular/core';
import { ViewEditContext } from './view.edit.context';

/**
 * Aggregate all context for use
 */
export interface ViewAggregationContext extends ViewEditContext {}
export const VIEW_CONTEXT = new InjectionToken<ViewAggregationContext>('VIEW_CONTEXT');
