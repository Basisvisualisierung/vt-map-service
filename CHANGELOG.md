## v1.1.0 (2020-07-31)
### Breaking changes
* Function _/search_params_ was removed, due to the new search functions of this service. Parameters for an external geocoder API are no longer requestable from the service.

### New Features
* New function _/suggest_ for address suggestions. The function expects one parameter _term_ for the search term.
* New function _/search_ for address search. The function expects one parameter _term_ for the search term.
* New configuration section _geocoder_ to configure the parameters for the external geocoder.

## v1.0.0 (2020-07-14)
### Breaking changes
* The section _services_ with the configuration parameters _root_url_, _root_path_ and _map_view_url_ was removed from configuration file _vt-map-service.yaml_.
* The _/map_ function now returns only the UUID of the saved map. The URLs for custom styles and applications are now created by VT Map Editor __v1.x__.

### New Features
* New function _/search_params_ that returns API parameters for a geolocation search. These API parameters are set by the environment variables _VTMS_SEARCH_API_ and _VTMS_SEARCH_API_KEY_.

## v0.5.0 (2020-03-09)
Initial release
