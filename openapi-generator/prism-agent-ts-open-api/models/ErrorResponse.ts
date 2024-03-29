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
/**
 * 
 * @export
 * @interface ErrorResponse
 */
export interface ErrorResponse {
    /**
     * The HTTP status code for this occurrence of the problem.
     * @type {number}
     * @memberof ErrorResponse
     */
    status: number;
    /**
     * A URI reference that identifies the problem type.
     * @type {string}
     * @memberof ErrorResponse
     */
    type: string;
    /**
     * A short, human-readable summary of the problem type. It does not change from occurrence to occurrence of the problem.
     * @type {string}
     * @memberof ErrorResponse
     */
    title: string;
    /**
     * A human-readable explanation specific to this occurrence of the problem.
     * @type {string}
     * @memberof ErrorResponse
     */
    detail?: string;
    /**
     * A URI reference that identifies the specific occurrence of the problem. It may or may not yield further information if dereferenced.
     * @type {string}
     * @memberof ErrorResponse
     */
    instance: string;
}

/**
 * Check if a given object implements the ErrorResponse interface.
 */
export function instanceOfErrorResponse(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "status" in value;
    isInstance = isInstance && "type" in value;
    isInstance = isInstance && "title" in value;
    isInstance = isInstance && "instance" in value;

    return isInstance;
}

export function ErrorResponseFromJSON(json: any): ErrorResponse {
    return ErrorResponseFromJSONTyped(json, false);
}

export function ErrorResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): ErrorResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'status': json['status'],
        'type': json['type'],
        'title': json['title'],
        'detail': !exists(json, 'detail') ? undefined : json['detail'],
        'instance': json['instance'],
    };
}

export function ErrorResponseToJSON(value?: ErrorResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'status': value.status,
        'type': value.type,
        'title': value.title,
        'detail': value.detail,
        'instance': value.instance,
    };
}

