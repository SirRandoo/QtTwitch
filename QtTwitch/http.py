# This file is part of QtTwitch.
#
# QtTwitch is free software:
# you can redistribute it
# and/or modify it under the
# terms of the GNU Lesser General
# Public License as published by
# the Free Software Foundation,
# either version 3 of the License,
# or (at your option) any later
# version.
#
# QtTwitch is distributed in
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without
# even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more
# details.
#
# You should have received a copy of the
# GNU Lesser General Public License along
# with QtTwitch.  If not,
# see <https://www.gnu.org/licenses/>.
import datetime
import json
import math
import typing

from PyQt5 import QtCore, QtNetwork

from QtUtilities import requests, signals

__all__ = ['Http']


class Http:
    """A HTTP class for interacting with Twitch's API.
    
    - All endpoint docstrings are taken from Twitch's API documentation."""
    # TODO: Properly handle clip creation ratelimits
    # TODO: Properly handle metadata ratelimits
    HELIX = 'https://api.twitch.tv/helix'
    
    def __init__(self, **kwargs):
        """
        :param client_id: The client id to use for requests.
        :param token: The token to use for authenticated requests.
        :param factory: The factory to use for requests.
        """
        # Public attributes
        self.client_id: typing.Optional[str] = kwargs.get('client_id')
        self.token: typing.Optional[str] = kwargs.get('token')
        self.factory: typing.Optional[requests.Factory] = kwargs.get('factory', requests.Factory())
    
    # Requests
    def request(self, op: str, endpoint: str = None, *,
                params: typing.Dict[str, typing.Union[str, typing.List[str]]] = None,
                headers: typing.Dict[str, str] = None, data: typing.Union[str, bytes, QtCore.QBuffer] = None,
                request: QtNetwork.QNetworkRequest = None):
        """Issues a new request to Twitch's API."""
        # Stitch the endpoint to the API url
        api = QtCore.QUrl(self.HELIX)
        path = api.path().rstrip('/')
        
        api.setPath(f'{path}/{endpoint}')
        
        # Stitch the url query
        q = QtCore.QUrlQuery()
        
        # Add the parameters to the query
        for key, value in params.items():
            if isinstance(value, list):
                for v in value:
                    q.addQueryItem(key, v)
            
            else:
                q.addQueryItem(key, value)
        
        # Assign the query to the url
        api.setQuery(q)
        
        # Create a request object if it does not exist
        if request is None:
            request = QtNetwork.QNetworkRequest(api)
            
            # Populate the request's headers
            for key, value in headers.items():
                request.setRawHeader(key.encode(), value.encode())
        
        # Ensure the Twitch API headers exist
        if not request.hasRawHeader(b'Client-ID'):
            request.setRawHeader(b'Client-ID', self.client_id.encode())
        
        if not request.hasRawHeader(b'Authorization'):
            request.setRawHeader(b'Authorization', f'OAuth {self.token}'.encode())
        
        return self._request(op, request, data=data).json()
    
    def _request(self, op: str, request: QtNetwork.QNetworkRequest,
                 data: typing.Union[typing.AnyStr, QtCore.QByteArray] = None) -> requests.Response:
        """Truly initiates the network request."""
        # Initiate the request
        reply = self.factory.request(op, request=request, data=data)
        
        # If we're being ratelimited, wait the specified
        # amount of time, then reinitiate the request.
        if reply.code == 429:
            timeout = reply.headers['Ratelimit-Reset']  # Get the ratelimit reset
            date = datetime.datetime.fromtimestamp(timeout, tz=datetime.timezone.utc)  # Convert it to a datetime object
            diff = date - datetime.datetime.now(tz=datetime.timezone.utc)  # Get a timedelta object
            
            timer = QtCore.QTimer()
            
            # Start a timer that ends after the difference's total seconds rounded up
            timer.start(int(math.ceil(diff.total_seconds() * 1000, 0)))
            signals.wait_for_signal(timer.timeout)
            
            # Stop and delete the timer once it ticks once
            timer.stop()
            timer.deleteLater()
            
            # Redo the request
            return self._request(op, request, data=data)
        
        return reply
    
    # Utility methods
    @staticmethod
    def _stitch_params(**kwargs):
        """Returns passed parameters without None values."""
        return {k: v for k, v in kwargs.items() if v is not None}
    
    # Endpoints
    def validate_token(self, token: str):
        """Validates a token."""
        # Declarations
        req = QtNetwork.QNetworkRequest(QtCore.QUrl('https://id.twitch.tv/oauth2/validate'))
        req.setRawHeader(b'Authorization', b'OAuth ' + token.encode())
        
        return self._request(op='GET', request=req).json()
    
    def get_extension_analytics(self, *, after: str = None, ended_at: str = None, extension_id: str = None,
                                first: int = None, started_at: str = None, type_: str = None):
        """Gets a URL that extension developers can use to download analytics
        reports (CSV files) for their extensions.  The URL is valid for 5
        minutes.
        
        If you specify a future date, the response will be "Report Not Found For
        Date Range."  If you leave both `started_at` and `ended_at` blank, the
        API returns the most recent date of data.
        
        * Required scope: `analytics:read:extensions`"""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        if type_ is not None and type_ not in ['overview_v1', 'overview_v2']:
            raise ValueError('Parameter "type_" can only be "overview_v1" or "overview_v2".')
        
        return self.request(
            'GET',
            'analytics/extensions',
            params=self._stitch_params(
                after=after,
                ended_at=ended_at,
                extension_id=extension_id,
                first=first,
                started_at=started_at,
                type=type_
            )
        )
    
    def get_game_analytics(self, *, after: str = None, ended_at: str = None, first: int = None, game_id: str = None,
                           started_at: str = None, type_: str = None):
        """Gets a URL that game developers can use to download analytics reports
        (CSV files) for their games.  The URL is valid for 5 minutes.
        
        The response has a JSON payload with a `data` field containing an array
        of games information elements and can contain a `pagination` field
        containing information required to query for more streams.
        
        If you specify a future date, the response will be "Report Not Found For
        Date Range."  If you leave both `started_at` and `ended_at` blank, the
        API returns the most recent date of data.
        
        * Required scope: `analytics:read:games`"""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        if type_ is not None and type_ not in ['overview_v1', 'overview_v2']:
            raise ValueError('Parameter "type_" can only be "overview_v1" or "overview_v2".')
        
        return self.request(
            'GET',
            'analytics/games',
            params=self._stitch_params(
                after=after,
                ended_at=ended_at,
                first=first,
                game_id=game_id,
                started_at=started_at,
                type=type_
            )
        )
    
    def get_bits_leaderboard(self, *, count: int = None, period: str = None,
                             started_at: str = None, user_id: str = None):
        """Gets the ranked list of Bits leaderboard information for an
        authorized broadcaster.
        
        * Required scope: `bits:read`"""
        if count is not None and count > 100:
            raise ValueError('Parameter "count" cannot be greater than 100.')
        
        if period is not None and period not in ['all', 'day', 'week', 'month', 'year']:
            raise ValueError('Parameter "period" can only be "all", "day", "week", "month", or "year"')
        
        return self.request(
            'GET',
            'bits/leaderboard',
            params=self._stitch_params(
                count=count,
                period=period,
                started_at=started_at,
                user_id=user_id
            )
        )
    
    def create_clip(self, broadcaster_id: str, *, has_delay: bool = None):
        """Creates a clip programmatically.  This returns both an ID and an edit
        URL for the new clip.
        
        Clip creation takes time.  We recommend that you query `Get Clips`, with
        the clip ID that is returned here.  If the Get Clips returns a valid
        clip, your clip creation was successful.  If, after 15 seconds, you
        still have not gotten back a valid clip from Get Clips, assume that the
        clip was not created and retry Create Clip.
        
        This endpoint has a global rate limit, across all callers.  The limit
        may change over time, but the response includes informative headers:
        
        +----------------------------------------+---------+
        |                    Name                |  Value  |
        +========================================+=========+
        | Ratelimit-Helixclipscreation-Limit     | integer |
        +----------------------------------------+---------+
        | Ratelimit-Helixclipscreation-Remaining | integer |
        +----------------------------------------+---------+
        
        * Required scope: `clips:edit`"""
        return self.request(
            'POST',
            'clips',
            params=self._stitch_params(
                broadcaster_id=broadcaster_id,
                has_delay=has_delay
            )
        )
    
    def get_clips(self, broadcaster_id: str = None, game_id: str = None,
                  id_: typing.Union[str, typing.List[str]] = None,
                  *, after: str = None, before: str = None, ended_at: str = None, first: int = None,
                  started_at: str = None):
        """Gets clip information by clip ID (one or more), broadcaster ID (one
        only), or game ID (one only).
        
        The response has a JSON payload with a data field containing an array
        of clip information elements and a pagination field containing
        information required to query for more streams."""
        if broadcaster_id is None and game_id is None and id_ is None:
            raise ValueError('Missing a required parameter (broadcaster_id, game_id, or id_ is required)')
        
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'clips',
            params=self._stitch_params(
                after=after,
                before=before,
                ended_at=ended_at,
                first=first,
                started_at=started_at
            )
        )
    
    def create_entitlement(self, manifest_id: str, type_: str = None):
        """Creates a URL where you can upload a manifest file and notify users
        that they have an entitlement.  Entitlements are digital items that
        users are entitled to use.  Twitch entitlements are granted to users
        gratis or as part of a purchase on Twitch.
        
        * Requires app access token"""
        if type_ is not None and type_ != 'bulk_drops_grant':
            raise ValueError('Parameter "type_" can only be bulk_drops_grant')
        
        if type_ is None:
            type_ = 'bulk_drops_grant'
        
        return self.request(
            'POST',
            'entitlements/upload',
            params=self._stitch_params(
                manifest_id=manifest_id,
                type=type_
            )
        )
    
    def get_code_status(self, code: typing.Union[str, typing.List[str]], user_id: int = None):
        """Gets the status of one or more provided codes.  This API requires
        that the caller is an authenticated Twitch user.  The API is throttled
        to one request per second per authenticated user.
        
        * Requires an app access token"""
        return self.request(
            'GET',
            'entitlements/codes',
            params=self._stitch_params(
                code=code,
                user_id=user_id
            )
        )
    
    def redeem_code(self, code: typing.Union[str, typing.List[str]], user_id: int = None):
        """The API requires that the caller is an authenticated Twitch user.
        The API is throttled to one request per second per authenticated user.
        
        * Requires an app access token"""
        return self.request(
            'POST',
            'entitlements/codes',
            params=self._stitch_params(
                code=code,
                user_id=user_id
            )
        )
    
    def get_top_games(self, *, after: str = None, before: str = None, first: int = None):
        """Gets games sorted by number of current viewers on Twitch, most
        popular first.
        
        Thee response has a JSON payload with a data field containing an array
        of games information elements and a pagination field containing
        information required to query for more streams."""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'games/top',
            params=self._stitch_params(
                after=after,
                before=before,
                first=first
            )
        )
    
    def get_games(self, id_: typing.Union[str, typing.List[str]] = None,
                  name: typing.Union[str, typing.List[str]] = None):
        """Gets game information by game ID or name.
        
        The response has a JSON payload with a data field containing an array of
        game elements."""
        if id_ is None and name is None:
            raise ValueError('Parameter "id_" and/or "name" must be specified.')
        
        return self.request(
            'GET',
            'games',
            params=self._stitch_params(
                id=id_,
                name=name
            )
        )
    
    def get_streams(self, *, after: str = None, before: str = None,
                    community_id: typing.Union[str, typing.List[str]] = None, first: int = None,
                    game_id: typing.Union[str, typing.List[str]] = None,
                    language: typing.Union[str, typing.List[str]] = None,
                    user_id: typing.Union[str, typing.List[str]] = None,
                    user_login: typing.Union[str, typing.List[str]] = None):
        """Gets information about active streams.  Streams are returned sorted
        by number of current viewers, in descending order.  Across multiple
        pages of results, there may be duplicate or missing streams, as viewers
        join and leave streams.
        
        The response has a JSON payload with a data field containing an array
        of stream information elements and a pagination field containing
        information required to query for more streams."""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'streams',
            params=self._stitch_params(
                community_id=community_id,
                game_id=game_id,
                language=language,
                user_id=user_id,
                user_login=user_login,
                after=after,
                before=before
            )
        )
    
    def get_streams_metadata(self, *, after: str = None, before: str = None,
                             community_id: typing.Union[str, typing.List[str]] = None, first: int = None,
                             game_id: typing.Union[str, typing.List[str]] = None,
                             language: typing.Union[str, typing.List[str]] = None,
                             user_id: typing.Union[str, typing.List[str]] = None,
                             user_login: typing.Union[str, typing.List[str]] = None):
        """Gets metadata information about active streams playing Overwatch or
        Hearthstone.  Streams are sorted by number of current viewers, in
        descending order.  Across multiple page of results, there may be
        duplicate or missing streams, as viewers join and leave streams.
        
        The response has a JSON payload with a data field containing an array
        of stream information elements and a pagination field containing
        information required to query for more streams.
        
        This endpoint has a global rate limit, across all callers.  The limit
        may change over time, but the response includes informative headers:
        
        +------------------------------------------+---------+
        |                     Name                 |  Value  |
        +==========================================+=========+
        | Ratelimit-Helixstreamsmetadata-Limit     | integer |
        +------------------------------------------+---------+
        | Ratelimit-Helixstreamsmetadata-Remaining | integer |
        +------------------------------------------+---------+
        """
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'streams/metadata',
            params=self._stitch_params(
                after=after,
                before=before,
                community_id=community_id,
                first=first,
                game_id=game_id,
                language=language,
                user_login=user_login,
                user_id=user_id
            )
        )
    
    def create_stream_marker(self, user_id: str, *, description: str = None):
        """Creates a `marker` in the stream of a user specified by a user ID.
        A marker is an arbitrary point in a stream that the broadcaster wants to
        mark;  e.g., to easily return to later.  The marker is created at the
        current timestamp in the live broadcast when the request is processed.
        Markers can be created by the stream owner or editors.  The user
        creating the marker is identified by a Bearer token.
        
        Markers cannot be created in some cases (an error will occur):
        
        - If the specified user's stream is not live.
        - If VOD (past broadcast) storage is not enabled for the stream.
        - For premieres (live, first-viewing events that combine uploaded videos
        with live chat).
        - For reruns (subsequent (not live) streaming of any past broadcast,
        including past premieres).
        
        * Required scope: `user:edit:broadcast`"""
        # Stitch the data body
        d = {'user_id': user_id}
        
        if description is not None:
            d['description'] = description
        
        return self.request('POST', 'streams/markers', data=json.dumps(d))
    
    def get_stream_markers(self, user_id, video_id: str = None, *, after: str = None, before: str = None,
                           first: int = None):
        """Gets a list of `markers` for either a specified user's most recent
        stream or a specified VOD/video (stream), ordered by recency.  A marker
        is an arbitrary point in a stream that the broadcaster wants to mark;
        e.g., to easily return to later.  The only markers are returned are
        those created by the user identified by the Bearer token.
        
        The response has a JSON payload with a data field containing an array of
        marker information elements and a pagination field containing
        information required to query for more follow information.
        
        * Required scope: `user:read:broadcast`"""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'streams/markers',
            params=self._stitch_params(
                user_id=user_id,
                video_id=video_id,
                after=after,
                before=before,
                first=first
            )
        )
    
    def get_broadcaster_subscriptions(self, broadcaster_id: str):
        """Gets all of a broadcaster's subscriptions.
        
        * Required scope: `channel:read:subscriptions`
        * Broadcasters can only request their own subscriptions"""
        return self.request(
            'GET',
            'subscriptions',
            params=self._stitch_params(
                broadcaster_id=broadcaster_id
            )
        )
    
    def get_broadcasters_subscribers(self, broadcaster_id: str, user_id: typing.Union[str, typing.List[str]] = None):
        """Gets broadcaster's subscriptions by user ID (one or more).
        
        * Required scope: `channel:read:subscriptions`
        * Users can only request their own subscriptions"""
        return self.request(
            'GET',
            'subscriptions',
            params=self._stitch_params(
                broadcaster_id=broadcaster_id,
                user_id=user_id
            )
        )
    
    def get_all_stream_tags(self, *, after: str = None, first: int = None, tag_id: typing.Union[str, typing.List[str]]):
        """Gets the list of all stream tags defined by Twitch, optionally
        filtered by tag ID(s).
        
        The response has a JSON payload with a data field containing an array
        of tag elements and a pagination field containing information required
        to query for more tags.
        
        * Requires app access token"""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'tags/streams',
            params=self._stitch_params(
                after=after,
                first=first,
                tag_id=tag_id
            )
        )
    
    def get_stream_tags(self, broadcaster_id: str):
        """Gets a list of tags for a specified stream (channel).
        
        The response has a JSON payload with a `data` field containing an array
        of tag elements.
        
        * Requires app access token"""
        return self.request(
            'GET',
            'streams/tags',
            params=self._stitch_params(broadcaster_id=broadcaster_id)
        )
    
    def replace_stream_tags(self, broadcaster_id: str, tag_ids: typing.List[str] = None):
        """Applies specified tags to a specified stream, overwriting any
        existing tags applied to that stream.  If no tags are specified, all
        tags previously applied to the stream are removed.  Automated tags are
        not affected by this operation.
        
        Tags expire 72 hours after they are applied, unless the stream is live
        within that time period.  If the stream is live within 72-hour window,
        the 72-hour clock restarts when the stream goes offline.  The expiration
        period is subject to change.
        
        * Required scope: `user:edit:broadcast`"""
        # The API only lets up to 5 tags be applied to a stream,
        # but the API supports up to 100 tag ids.  The 5 tag limit
        # should be enforced upstream.
        if tag_ids is not None and len(tag_ids) > 100:
            raise ValueError('Parameter "tag_ids" cannot contain more than 100 entries.')
        
        if tag_ids is not None:
            data = json.dumps({'tag_ids': tag_ids})
        
        else:
            data = None
        
        return self.request(
            'PUT',
            'streams/tags',
            params=self._stitch_params(broadcaster_id=broadcaster_id),
            data=data
        )
    
    def get_users(self, *, id_: typing.Union[str, typing.List[str]] = None,
                  login: typing.Union[str, typing.List[str]] = None):
        """Gets information about one or more specified Twitch users.  Users
        are identified by optional user IDs and/or login name.  If neither a
        user ID nor a login name is specified, the user is looked up by Bearer
        token.
        
        The response has a JSON payload with a `data` field containing an array
        of user-information elements.
        
        * Optional scope: `user:read:email`"""
        if id_ is not None and isinstance(id_, list) and len(id_) > 100:
            raise ValueError('Parameter "id_" cannot contain more than 100 values.')
        
        if login is not None and isinstance(login, list) and len(login) > 100:
            raise ValueError('Parameter "login" cannot contain more than 100 values.')
        
        return self.request(
            'GET',
            'users',
            params=self._stitch_params(id=id, login=login)
        )
    
    def get_users_follows(self, *, after: str = None, first: int = None, from_id: str = None, to_id: str = None):
        """Gets information on follow relationships between two Twitch users.
        Information returned is sorted in order, most recent follow first.  This
        can return information like "who is lirik following," "who is following
        lirik," or "is user X following user Y."
        
        This response has a JSON payload with a data field containing an array
        of follow relationship elements and a pagination field containing
        information required to query for more follow information."""
        if from_id is None and to_id is None:
            raise ValueError('"from_id" and/or "to_id" must be provided.')
        
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'users/follows',
            params=self._stitch_params(
                after=after,
                first=first,
                from_id=from_id,
                to_id=to_id
            )
        )
    
    def update_user(self, description: str):
        """Updates the description of a user specified by a Bearer token.
        
        * Required scope: `user:edit`"""
        return self.request('PUT', 'users', params={'description': description})
    
    def get_user_extensions(self):
        """Gets a list of all extensions (both active and inactive) for a
        specified user, identified by a Bearer token.
        
        The response has JSON payload with a data field containing an array of
        user-information elements.
        
        * Required scope: `user:read:broadcast`"""
        return self.request('GET', 'users/extensions/list')
    
    def get_user_active_extensions(self, *, user_id: str = None):
        """Gets information about active extensions installed by a specified
        user, identified by a user ID or Bearer token.
        
        * Optional scope: `user:read:broadcast` or `user:edit:broadcast`"""
        return self.request('GET', 'users/extensions', params=self._stitch_params(user_id=user_id))
    
    def update_user_extensions(self, panel: typing.List[dict], overlay: typing.List[dict],
                               component: typing.List[dict]):
        """Updates the activation state, extension ID, and/or version number of
        installed extensions for a specified user, identified by a Bearer token.
        If you try to activate a given extension under multiple extension types,
        the last write wins (and there is no guarantee of write order).
        
        * Required scope: `user:edit:broadcast`"""
        data = {
            'panel': {str(i): d for i, d in enumerate(panel, start=1)},
            'overlay': {str(i): d for i, d in enumerate(overlay, start=1)},
            'component': {str(i): d for i, d in enumerate(component, start=1)}
        }
        
        return self.request(
            'PUT',
            'users/extensions',
            data=json.dumps(data)
        )
    
    def get_videos(self, id_: typing.Union[str, typing.List[str]] = None, user_id: str = None, game_id: str = None,
                   after: str = None, before: str = None, first: int = None,
                   language: str = None, period: str = None, sort: str = None, type_: str = None):
        """Gets video information by video ID (one or more), user ID (one only),
        or game ID (one only).
        
        The response has a JSON payload with a data field containing an array of
        video elements.  For lookup by user or game, pagination is available,
        along with several filters that can be specified as query string
        parameters."""
        if id_ is None and user_id is None and game_id is None:
            raise ValueError('"id_", "user_id", and/or "game_id" must be specified.')
        
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        if period is not None and period not in ['all', 'day', 'week', 'month']:
            raise ValueError('Parameter "period" can only be all, day, week, or month.')
        
        if sort is not None and sort not in ['time', 'trending', 'views']:
            raise ValueError('Parameter "sort" can only be time, trending, or views.')
        
        if type_ is not None and type_ not in ['all', 'upload', 'archive', 'highlight']:
            raise ValueError('Parameter "type_" can only be all, upload, archive, or highlight.')
        
        return self.request(
            'GET',
            'videos',
            params=self._stitch_params(
                id=id_,
                user_id=user_id,
                game_id=game_id,
                after=after,
                before=before,
                first=first,
                language=language,
                period=period,
                sort=sort,
                type=type_
            )
        )
    
    def get_webhook_subscriptions(self, *, after: str = None, first: int = None):
        """Gets the Webhook subscriptions of user identified by a Bearer token,
        in order of expiration.
        
        The response has a JSON payload with a data field containing an array of
        subscription elements and a pagination field containing information
        required to query for more subscriptions.
        
        * Requires app access token"""
        if first is not None and first > 100:
            raise ValueError('Parameter "first" cannot be greater than 100.')
        
        return self.request(
            'GET',
            'webhooks/subscriptions',
            params=self._stitch_params(
                after=after,
                first=first
            )
        )
