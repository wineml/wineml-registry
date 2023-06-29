import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import serviceCaller from '../service'
import {
  Box,
  Group,
  Stack,
  Select,
  Card,
  Text,
  Input,
  Badge,
  createStyles,
  Skeleton,
} from '@mantine/core';
import { useInputState } from '@mantine/hooks';
import { IconFilterX } from '@tabler/icons-react';

const useStyles = createStyles((theme) => ({
  card: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white,
  },

  label: {
    textTransform: 'uppercase',
    fontSize: theme.fontSizes.xs,
    fontWeight: 700,
  },
}));

export function generateLightColor(text, lightness = 80) {
  const hash = Array.from(text).reduce((hash, char) => ((hash << 5) - hash) + char.charCodeAt(0), 0);
  const hue = hash % 360;
  const saturation = 100;
  const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  return color;
}

function Models() {
  const { classes, theme } = useStyles();
  const navigate = useNavigate();
  const [allModelCards, setAllModelCards] = useState([]);
  const [namespaces, setNamespaces] = useState([""]);
  const [selectedNamespace, setSelectedNamespace] = useState(null);
  const [modelsInNamespace, setModelsInNamespace] = useState([{}]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterString, setFilterString] = useInputState('');

  useEffect(() => {
    serviceCaller.get({ route: '/model/all' })
        .then((res) => {
          let uniqueNamespaces = [...new Set(res.data.map((modelCard) => modelCard.namespace))];
          setAllModelCards(res.data);
          setNamespaces(uniqueNamespaces);
          setSelectedNamespace(uniqueNamespaces[0]);
          setIsLoading(false);
        }
      ).catch((err) => {
        setIsLoading(false);
        }
      );
  }, []);

  useEffect(() => {
    setModelsInNamespace(allModelCards.filter((modelCard) => (
      modelCard.namespace === selectedNamespace) && (modelCard.model_name.toLowerCase().includes(filterString)
      )));
  }, [selectedNamespace, allModelCards, filterString]);

  function handleModelClick(modelCard) {
    navigate(`/model/${modelCard.id}`)
  }

  function handleTagClick(event, tag) {
    event.stopPropagation();
    console.log(tag);
  }

  return (
    <Box>
      <Group>
      {
        isLoading ? <Skeleton height={40} width={160} /> :
          <Select
            label="Namespace"
            value={selectedNamespace}
            onChange={setSelectedNamespace}
            data={namespaces}
            styles={() => ({
              item: {
                '&[data-selected]': {
                  '&, &:hover': {
                    backgroundColor: "#63032e",
                    color: "white",
                  },
                },
              },
              input: {
                '&:focus-within': {
                  borderColor: "#63032e",
                },
              },
            })}
            sx={{
              width: 160,
              mb: 3,
              marginTop: -10,
            }}
        />
      }
      {
        isLoading ? <Skeleton height={40} width={160} /> :
        <Input
          icon={<IconFilterX size="1.125rem" />}
          placeholder="Filter"
          value={filterString}
          onChange={setFilterString}
          styles={() => ({
            input: {
              '&:focus-within': {
                borderColor: "#63032e",
              },
            },
          })}
          sx={{
            marginTop: 15,
            flexGrow: 1,
          }}
        />
      }
      </Group>
      <Stack pt={20} spacing={10}>
      {
        isLoading ?
        Array.from({ length: 20 }).map((_, index) => (
          <Skeleton key={index} height={55} width="100%"/>
        )) :
        modelsInNamespace.map((modelCard, i) => (
        <Card p={15} withBorder shadow='sm' key={`model-${i}`} radius="sm" className={classes.card}>
          <Card.Section
            sx={{
              '&:hover': {
                cursor: 'pointer',
                backgroundColor: theme.fn.lighten("#63032e", 0.95),
              },
            }}
            onClick={() => handleModelClick(modelCard)}
          >
            <Group position="apart">
              <Text p={15} fw={500}>
                {modelCard.model_name}
              </Text>
              <Group spacing={7} pr={15}>
              {
                modelCard.tags?.map((tag, i) => {
                  let tagColor = generateLightColor(tag);
                  let tagHoverColor = "#63032e"
                  return (
                    <Badge
                      sx={{
                        backgroundColor: tagColor,
                        color: 'black',
                        '&:hover': {
                          background: tagHoverColor,
                          color: 'white'
                        },
                      }}
                      key={`${modelCard.model_name}-tag-${i}`}
                      label={tag}
                      onClick={(event) => {handleTagClick(event, tag)}}
                    >
                      {tag}
                    </Badge>
                  )
                })
              }
              </Group>
              </Group>
            </Card.Section>
          </Card>
        ))
      }
      </Stack>
    </Box>
  );
}

export default Models;
