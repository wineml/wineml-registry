import { useEffect, useState } from 'react';
import serviceCaller from '../service';
import { useParams } from 'react-router-dom';
import {
    createStyles,
    Table,
    Group,
    ScrollArea,
    rem,
    Box,
    Stack,
    Text,
    Center,
    Badge,
    UnstyledButton,
} from '@mantine/core';
import { IconSelector, IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { generateLightColor } from './models';


const useStyles = createStyles((theme) => ({
    progressBar: {
      '&:not(:first-of-type)': {
        borderLeft: `${rem(3)} solid ${
          theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white
        }`,
      },
    },
  }));

function Th({ children, reversed, sorted, onSort }) {
    const { classes } = useStyles();
    const Icon = sorted ? (reversed ? IconChevronUp : IconChevronDown) : IconSelector;
    return (
        <th className={classes.th}>
        <UnstyledButton onClick={onSort} className={classes.control}>
            <Group position="apart">
            <Text fw={500} fz="sm">
                {children}
            </Text>
            <Center className={classes.icon}>
                <Icon size="0.9rem" stroke={1.5} />
            </Center>
            </Group>
        </UnstyledButton>
        </th>
    );
}

function sortData(data, payload) {
    const { sortBy } = payload;

    if (!sortBy) {
      return data;
    }

    return [...data].sort((a, b) => {
        if (payload.reversed) {
          return b[sortBy].localeCompare(a[sortBy]);
        }

        return a[sortBy].localeCompare(b[sortBy]);
      });
  }

function formatDatetime(datetimeString) {
    const datetime = new Date(datetimeString);

    const options = {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    };

    return datetime.toLocaleString(undefined, options);
}



function Model() {
    const params = useParams();
    const [modelInfo, setModelInfo] = useState({});
    const [modelVersions, setModelVersions] = useState([]);
    const [sortedData, setSortedData] = useState([]);
    const [sortBy, setSortBy] = useState('last_updated');
    const [reverseSortDirection, setReverseSortDirection] = useState(false);
    let modelID = params.modelID;

    const setSorting = (field) => {
        const reversed = field === sortBy ? !reverseSortDirection : false;
        setReverseSortDirection(reversed);
        setSortBy(field);
        setSortedData(sortData(modelVersions, { sortBy: field, reversed }));
    };

    useEffect(() => {
        serviceCaller.get({
            route: `/model/${modelID}`,
            params: {}
        }).then((res) => {
            setModelInfo(res.data);
          }
        );
    }, [modelID]);

    useEffect(() => {
        if (Object.keys(modelInfo).length !== 0) {
            serviceCaller.get({
                route: `/modelversion/all`,
                params: {
                    namespace: modelInfo.namespace,
                    model_name: modelInfo.model_name,
                }}).then((res) => {
                    setModelVersions(res.data);
                    setSortedData(res.data);
                });
        }
    }, [modelInfo]);

    const rows = sortedData.map((modelversion, i) => {
        let statusColor = generateLightColor(modelversion.model_status);
        return (
          <tr key={modelversion.model_version}>
            <td>{modelversion.model_version}</td>
            <td>
                <Badge
                    sx={{
                        backgroundColor: statusColor,
                        color: 'black',
                    '&:hover': {
                        cursor: 'pointer',
                    },
                    }}
                    key={`${modelInfo.model_name}-model_status-${i}`}
                    label={modelversion.model_status}
                    onClick={() => console.log(modelversion.model_status)}
                    >
                    {modelversion.model_status}
                </Badge>
            </td>
            <td>{formatDatetime(modelversion.created_at)}</td>
            <td>{formatDatetime(modelversion.last_updated)}</td>
          </tr>
        );
      });

      return (
        <Box>
            <Stack spacing={0}>
                <Group position="apart">
                    <Text size={45} fw={600}>{modelInfo.model_name}</Text>
                    <Text size={20} fw={200}>{modelInfo.namespace}</Text>
                </Group>
                <Group>
                {
                modelInfo.tags?.map((tag, i) => {
                  let tagColor = generateLightColor(tag);
                  let tagHoverColor = "#63032e"
                  return (
                    <Badge
                      sx={{
                        backgroundColor: tagColor,
                        color: 'black',
                        '&:hover': {
                            cursor: 'pointer',
                            background: tagHoverColor,
                            color: 'white'
                        },
                      }}
                      key={`${modelInfo.model_name}-tag-${i}`}
                      label={tag}
                      onClick={() => console.log(tag)}
                    >
                      {tag}
                    </Badge>
                  )
                })
                }
                </Group>
            </Stack>
            <ScrollArea>
            <Table verticalSpacing={5} mt={20}>
                <thead>
                <tr>
                    <Th
                        sorted={sortBy === 'model_version'}
                        reversed={reverseSortDirection}
                        onSort={() => setSorting('model_version')}
                    >
                        Version
                    </Th>
                    <th>Status</th>
                    <Th
                        sorted={sortBy === 'created_at'}
                        reversed={reverseSortDirection}
                        onSort={() => setSorting('created_at')}
                    >
                        Created
                    </Th>
                    <Th
                        sorted={sortBy === 'last_updated'}
                        reversed={reverseSortDirection}
                        onSort={() => setSorting('last_updated')}
                    >
                        Last Updated
                    </Th>
                </tr>
                </thead>
                <tbody>{rows}</tbody>
            </Table>
            </ScrollArea>
        </Box>
      );
}

export default Model;
