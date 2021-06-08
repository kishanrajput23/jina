import os

import numpy as np
import pytest

from jina import Flow, Document

cur_dir = os.path.dirname(os.path.abspath(__file__))

CLOUD_HOST = 'localhost:8000'  # consider it as the staged version
NUM_DOCS = 100


@pytest.fixture()
def docker_image():
    img_name = 'test-mwu-encoder'
    import docker

    client = docker.from_env()
    client.images.build(
        path=os.path.join(cur_dir, '../../unit/mwu-encoder/'), tag=img_name
    )
    client.close()
    yield img_name
    client = docker.from_env()
    client.containers.prune()


@pytest.mark.parametrize('parallels', [1, 2])
def test_r_l_docker(parallels, docker_image, mocker):
    response_mock = mocker.Mock()
    f = (
        Flow()
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels,
             timeout_ready=-1)
        .add(parallel=parallels)
    )
    with f:
        f.index(
            inputs=(Document(text='hello') for _ in range(NUM_DOCS)),
            on_done=response_mock,
        )

    response_mock.assert_called()


@pytest.mark.parametrize('parallels', [1, 2])
def test_l_r_docker(parallels, docker_image, mocker):
    response_mock = mocker.Mock()

    f = (
        Flow()
        .add(parallel=parallels)
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
    )
    with f:
        f.index(
            inputs=(Document(text='hello') for _ in range(NUM_DOCS)),
            on_done=response_mock,
        )
    response_mock.assert_called()


@pytest.mark.parametrize('parallels', [1, 2])
def test_r_l_r_docker(parallels, docker_image, mocker):
    response_mock = mocker.Mock()

    f = (
        Flow()
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
        .add()
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
    )
    with f:
        f.index(
            inputs=(Document(text='hello') for _ in range(NUM_DOCS)),
            on_done=response_mock,
        )
    response_mock.assert_called()


@pytest.mark.skip('streaming gets stuck')
@pytest.mark.parametrize('parallels', [1])
def test_r_r_r_docker(parallels, docker_image, mocker):
    response_mock = mocker.Mock()

    f = (
        Flow()
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
        .add(uses=f'docker://{docker_image}',
             host=CLOUD_HOST,
             parallel=parallels)
    )
    with f:
        f.index(
            inputs=(Document(text='hello') for _ in range(NUM_DOCS)),
            on_done=response_mock,
        )
    response_mock.assert_called()


@pytest.mark.parametrize('parallels', [1, 2])
def test_l_r_l_docker(parallels, docker_image, mocker):
    response_mock = mocker.Mock()
    f = (
        Flow()
        .add()
        .add(
            uses=f'docker://{docker_image}',
            host=CLOUD_HOST,
            parallel=parallels)
        .add()
    )
    with f:
        f.index(
            inputs=(Document(blob=np.random.random([1, 100])) for _ in range(NUM_DOCS)),
            on_done=response_mock,
        )
    response_mock.assert_called()
