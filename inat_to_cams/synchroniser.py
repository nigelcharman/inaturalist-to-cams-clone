#  ====================================================================
#  Copyright 2023 EcoNet.NZ
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ====================================================================

import logging


from inat_to_cams import cams_writer, inaturalist_reader, translator  # setup_logging, translator


class INatToCamsSynchroniser:
    def sync_observation(self, observation):
        logging.info('-' * 80)
        logging.info(f'Syncing iNaturalist observation {observation}')
        inat_observation = inaturalist_reader.INatReader.flatten(observation)
        logging.info(f'Observed on {inat_observation.observed_on}')

        if not inat_observation:
            return

        inat_to_cams_translator = translator.INatToCamsTranslator()
        cams_observation = inat_to_cams_translator.translate(inat_observation)

        if not cams_observation:
            return

        writer = cams_writer.CamsWriter()
        global_id = writer.write_observation(cams_observation)

        return cams_observation, global_id
