import { InjectionToken } from '@angular/core';
import { ViewContext } from './view.context';
import { ViewDataType } from './view.type';

/**
 * The `ViewEditContext` abstract class extends the `ViewContext` class and provides
 * an interface for managing the lifecycle of an item within a view. It includes
 * methods for saving, removing, and canceling updates or creations of items.
 *
 * @abstract
 * @extends {ViewContext}
 */
export abstract class ViewEditContext extends ViewContext {
  /**
   * Saves the current item in
   */
  abstract save(filter?: ViewDataType, onError?: (message: string) => void): void;

  /**
   * Removes the current item from the view.
   */
  abstract remove(filter?: ViewDataType, onError?: (message: string) => void): void;

  /**
   * Cancels the current operation.
   */
  abstract cancel(filter?: ViewDataType, onError?: (message: string) => void): void;
}
export const VIEW_EDIT_CONTEXT = new InjectionToken<ViewEditContext>('VIEW_EDIT_CONTEXT');
