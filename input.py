# Standard
import json
import configparser
from datetime import datetime
# External
import pytz
# Internal
from shared import handle_error


class InputHandler:
    def __init__(self, args):
        self.args = args
        self.config = configparser.ConfigParser(inline_comment_prefixes="#")
        self.config.read('config.ini')
        self.domain = None
        self.server_id = None
        self.start_date = None
        self.timezone = None
        self.user_aliases = None
        self.min_games_required = None
        self.last_days_threshold = None
        self.min_games_last_days = None
        self.discard_ties = None
        self.decay_enabled = None
        self.decay_amount = None
        self.grace_days = None
        self.max_decay_proportion = None
        self.default_sigma = None
        self.default_mu = None
        self.verbose_output = None
        self.top_x = None
        self.write_txt = None
        self.write_csv = None
        self.json_file = None

    def set_handler(self):
        # Inputs (override with command-line arguments if provided)
        self.domain = self.args.domain or self.config.get('MANDATORY', 'DOMAIN')
        self.server_id = self.args.server_id or self.config.get('MANDATORY', 'SERVER_ID')
        self.start_date = self.args.date_start or self.config.get('MANDATORY', 'DATE_START')
        timezone_in = self.args.timezone or self.config.get('SETTINGS', 'TIMEZONE')
        self.timezone = pytz.timezone(timezone_in)
        self.user_aliases = json.loads(self.config.get('ALIAS_MAPPINGS', 'ALIASED_PLAYERS'))

        self.min_games_required = self.args.min_games or self.config.getint('PLAYER_FILTERING', 'MINIMUM_GAMES_REQUIRED')
        self.last_days_threshold = self.args.last_days_threshold or self.config.getint('PLAYER_FILTERING', 'LAST_DAYS_THRESHOLD')
        self.min_games_last_days = self.args.min_games_last_days or self.config.getint('PLAYER_FILTERING', 'MINIMUM_GAMES_LAST_DAYS')
        self.top_x = self.args.top_x or self.config.getint('PLAYER_FILTERING', 'TOP_X_CUTOFF')

        self.discard_ties = self.args.discard_ties or self.config.getboolean('MATCH_FILTERING', 'DISCARD_TIES')
        self.decay_enabled = self.args.decay_enabled or self.config.getboolean('SIGMA_DECAY', 'DECAY_ENABLED')
        self.decay_amount = self.args.decay_amount or self.config.getfloat('SIGMA_DECAY', 'DECAY_AMOUNT')
        self.grace_days = self.args.grace_days or self.config.getint('SIGMA_DECAY', 'DECAY_GRACE_DAYS')
        self.max_decay_proportion = self.args.max_decay_proportion or self.config.getfloat('SIGMA_DECAY', 'MAX_DECAY_PROPORTION')

        self.default_sigma = self.args.ts_default_sigma or self.config.getfloat('TRUESKILL', 'TS_DEFAULT_SIGMA')
        self.default_mu = self.args.ts_default_mu or self.config.getfloat('TRUESKILL', 'TS_DEFAULT_MU')

        self.verbose_output = self.args.verbose_output or self.config.getboolean('OUTPUT', 'VERBOSE_OUTPUT')
        self.write_txt = self.args.write_txt or self.config.getboolean('SETTINGS', 'WRITE_TXT')
        self.write_csv = self.args.write_csv or self.config.getboolean('SETTINGS', 'WRITE_CSV')
        self.json_file = self.args.json_file or self.config.get('ALTERNATIVE', 'JSON_FILENAME')

        self.validate_inputs()

    def validate_inputs(self):
        if not self.domain:
            handle_error(ValueError("DOMAIN not specified"), "Domain must be provided.")
        if not self.server_id:
            handle_error(ValueError("SERVER_ID not specified"), "Server ID must be provided.")
        if not self.start_date.isdigit() or len(self.start_date) != 13:
            handle_error(ValueError("DATE_START format error"), "Start date must be a 13-digit timestamp.")
        try:
            datetime.fromtimestamp(int(self.start_date) / 1000, self.timezone)
        except Exception as e:
            handle_error(e, "Invalid DATE_START timestamp.")
        if self.min_games_required < 0:
            handle_error(ValueError("MINIMUM_GAMES_REQUIRED must be non-negative"), "Minimum games required must be non-negative.")
        if self.last_days_threshold < 0:
            handle_error(ValueError("LAST_DAYS_THRESHOLD must be non-negative"), "Last days threshold must be non-negative.")
        if self.min_games_last_days < 0:
            handle_error(ValueError("MINIMUM_GAMES_LAST_DAYS must be non-negative"), "Minimum games in last days must be non-negative.")
        if self.top_x < 0:
            handle_error(ValueError("TOP_X_CUTOFF must be non-negative"), "Top X players cutoff must be non-negative.")
        if self.decay_amount < 0:
            handle_error(ValueError("DECAY_AMOUNT must be non-negative"), "Decay amount must be non-negative.")
        if self.grace_days < 0:
            handle_error(ValueError("DECAY_GRACE_DAYS must be non-negative"), "Grace days must be non-negative.")
        if not 0 <= self.max_decay_proportion <= 1:
            handle_error(ValueError("MAX_DECAY_PROPORTION must be between 0 and 1"), "Max decay proportion must be between 0 and 1.")
        if self.default_sigma <= 0:
            handle_error(ValueError("TS_DEFAULT_SIGMA must be positive"), "Default sigma for TrueSkill must be positive.")
        if self.default_mu <= 0:
            handle_error(ValueError("TS_DEFAULT_MU must be positive"), "Default mu for TrueSkill must be positive.")

    def get_settings(self):
        return {
            "domain": self.domain,
            "server_id": self.server_id,
            "start_date": self.start_date,
            "timezone": self.timezone,
            "user_aliases": self.user_aliases,
            "min_games_required": self.min_games_required,
            "last_days_threshold": self.last_days_threshold,
            "min_games_last_days": self.min_games_last_days,
            "discard_ties": self.discard_ties,
            "decay_enabled": self.decay_enabled,
            "decay_amount": self.decay_amount,
            "grace_days": self.grace_days,
            "max_decay_proportion": self.max_decay_proportion,
            "default_sigma": self.default_sigma,
            "default_mu": self.default_mu,
            "verbose_output": self.verbose_output,
            "top_x": self.top_x,
            "write_txt": self.write_txt,
            "write_csv": self.write_csv,
            "json_file": self.json_file
        }
