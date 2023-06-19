/* tslint:disable */
/* eslint-disable */
/**
 * Prism Agent
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { Connection } from './Connection';
import {
    ConnectionFromJSON,
    ConnectionFromJSONTyped,
    ConnectionToJSON,
} from './Connection';

/**
 * 
 * @export
 * @interface ConnectionsPage
 */
export interface ConnectionsPage {
    /**
     * 
     * @type {Array<Connection>}
     * @memberof ConnectionsPage
     */
    contents?: Array<Connection>;
    /**
     * 
     * @type {string}
     * @memberof ConnectionsPage
     */
    kind: string;
    /**
     * 
     * @type {string}
     * @memberof ConnectionsPage
     */
    self: string;
    /**
     * 
     * @type {string}
     * @memberof ConnectionsPage
     */
    pageOf: string;
    /**
     * 
     * @type {string}
     * @memberof ConnectionsPage
     */
    next?: string;
    /**
     * 
     * @type {string}
     * @memberof ConnectionsPage
     */
    previous?: string;
}

/**
 * Check if a given object implements the ConnectionsPage interface.
 */
export function instanceOfConnectionsPage(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "kind" in value;
    isInstance = isInstance && "self" in value;
    isInstance = isInstance && "pageOf" in value;

    return isInstance;
}

export function ConnectionsPageFromJSON(json: any): ConnectionsPage {
    return ConnectionsPageFromJSONTyped(json, false);
}

export function ConnectionsPageFromJSONTyped(json: any, ignoreDiscriminator: boolean): ConnectionsPage {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'contents': !exists(json, 'contents') ? undefined : ((json['contents'] as Array<any>).map(ConnectionFromJSON)),
        'kind': json['kind'],
        'self': json['self'],
        'pageOf': json['pageOf'],
        'next': !exists(json, 'next') ? undefined : json['next'],
        'previous': !exists(json, 'previous') ? undefined : json['previous'],
    };
}

export function ConnectionsPageToJSON(value?: ConnectionsPage | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'contents': value.contents === undefined ? undefined : ((value.contents as Array<any>).map(ConnectionToJSON)),
        'kind': value.kind,
        'self': value.self,
        'pageOf': value.pageOf,
        'next': value.next,
        'previous': value.previous,
    };
}

